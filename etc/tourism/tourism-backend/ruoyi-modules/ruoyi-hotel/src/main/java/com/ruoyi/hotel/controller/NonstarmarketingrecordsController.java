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
import com.ruoyi.hotel.domain.Nonstarmarketingrecords;
import com.ruoyi.hotel.service.INonstarmarketingrecordsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 非星级酒店营销记录Controller
 * 
 * @author ningf
 * @date 2024-07-14
 */
@RestController
@RequestMapping("/nonstarmarketingrecords")
public class NonstarmarketingrecordsController extends BaseController
{
    @Autowired
    private INonstarmarketingrecordsService nonstarmarketingrecordsService;

    /**
     * 查询非星级酒店营销记录列表
     */
    @RequiresPermissions("hotel:nonstarmarketingrecords:list")
    @GetMapping("/list")
    public TableDataInfo list(Nonstarmarketingrecords nonstarmarketingrecords)
    {
        startPage();
        List<Nonstarmarketingrecords> list = nonstarmarketingrecordsService.selectNonstarmarketingrecordsList(nonstarmarketingrecords);
        return getDataTable(list);
    }

    /**
     * 导出非星级酒店营销记录列表
     */
    @RequiresPermissions("hotel:nonstarmarketingrecords:export")
    @Log(title = "非星级酒店营销记录", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Nonstarmarketingrecords nonstarmarketingrecords)
    {
        List<Nonstarmarketingrecords> list = nonstarmarketingrecordsService.selectNonstarmarketingrecordsList(nonstarmarketingrecords);
        ExcelUtil<Nonstarmarketingrecords> util = new ExcelUtil<Nonstarmarketingrecords>(Nonstarmarketingrecords.class);
        util.exportExcel(response, list, "非星级酒店营销记录数据");
    }

    /**
     * 获取非星级酒店营销记录详细信息
     */
    @RequiresPermissions("hotel:nonstarmarketingrecords:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(nonstarmarketingrecordsService.selectNonstarmarketingrecordsById(id));
    }

    /**
     * 新增非星级酒店营销记录
     */
    @RequiresPermissions("hotel:nonstarmarketingrecords:add")
    @Log(title = "非星级酒店营销记录", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Nonstarmarketingrecords nonstarmarketingrecords)
    {
        return toAjax(nonstarmarketingrecordsService.insertNonstarmarketingrecords(nonstarmarketingrecords));
    }

    /**
     * 修改非星级酒店营销记录
     */
    @RequiresPermissions("hotel:nonstarmarketingrecords:edit")
    @Log(title = "非星级酒店营销记录", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Nonstarmarketingrecords nonstarmarketingrecords)
    {
        return toAjax(nonstarmarketingrecordsService.updateNonstarmarketingrecords(nonstarmarketingrecords));
    }

    /**
     * 删除非星级酒店营销记录
     */
    @RequiresPermissions("hotel:nonstarmarketingrecords:remove")
    @Log(title = "非星级酒店营销记录", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(nonstarmarketingrecordsService.deleteNonstarmarketingrecordsByIds(ids));
    }
}
