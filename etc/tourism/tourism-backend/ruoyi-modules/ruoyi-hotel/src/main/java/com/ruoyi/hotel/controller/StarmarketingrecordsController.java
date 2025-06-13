package com.ruoyi.hotel.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.hotel.domain.Starmarketingrecords;
import com.ruoyi.hotel.service.IStarmarketingrecordsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 酒店营销记录Controller
 * 
 * @author ningf
 * @date 2024-07-10
 */
@RestController
@RequestMapping("/starmarketingrecords")
public class StarmarketingrecordsController extends BaseController
{
    @Autowired
    private IStarmarketingrecordsService starmarketingrecordsService;

    /**
     * 查询酒店营销记录列表
     */
    @RequiresPermissions("hotel:starmarketingrecords:list")
    @GetMapping("/list")
    public TableDataInfo list(Starmarketingrecords starmarketingrecords)
    {
        startPage();
        List<Starmarketingrecords> list = starmarketingrecordsService.selectStarmarketingrecordsList(starmarketingrecords);
        return getDataTable(list);
    }

    /**
     * 导出酒店营销记录列表
     */
    @RequiresPermissions("hotel:starmarketingrecords:export")
    @Log(title = "酒店营销记录", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Starmarketingrecords starmarketingrecords)
    {
        List<Starmarketingrecords> list = starmarketingrecordsService.selectStarmarketingrecordsList(starmarketingrecords);
        ExcelUtil<Starmarketingrecords> util = new ExcelUtil<Starmarketingrecords>(Starmarketingrecords.class);
        util.exportExcel(response, list, "酒店营销记录数据");
    }

    /**
     * 获取酒店营销记录详细信息
     */
    @RequiresPermissions("hotel:starmarketingrecords:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(starmarketingrecordsService.selectStarmarketingrecordsById(id));
    }

    /**
     * 新增酒店营销记录
     */
    @RequiresPermissions("hotel:starmarketingrecords:add")
    @Log(title = "酒店营销记录", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Starmarketingrecords starmarketingrecords)
    {
        return toAjax(starmarketingrecordsService.insertStarmarketingrecords(starmarketingrecords));
    }

    /**
     * 修改酒店营销记录
     */
    @RequiresPermissions("hotel:starmarketingrecords:edit")
    @Log(title = "酒店营销记录", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Starmarketingrecords starmarketingrecords)
    {
        return toAjax(starmarketingrecordsService.updateStarmarketingrecords(starmarketingrecords));
    }

    /**
     * 删除酒店营销记录
     */
    @RequiresPermissions("hotel:starmarketingrecords:remove")
    @Log(title = "酒店营销记录", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(starmarketingrecordsService.deleteStarmarketingrecordsByIds(ids));
    }
}
