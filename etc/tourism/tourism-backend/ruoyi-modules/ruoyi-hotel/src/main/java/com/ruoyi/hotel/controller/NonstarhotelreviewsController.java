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
import com.ruoyi.hotel.domain.Nonstarhotelreviews;
import com.ruoyi.hotel.service.INonstarhotelreviewsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 非星级酒店评价Controller
 * 
 * @author ningf
 * @date 2024-07-15
 */
@RestController
@RequestMapping("/nonstarhotelreviews")
public class NonstarhotelreviewsController extends BaseController
{
    @Autowired
    private INonstarhotelreviewsService nonstarhotelreviewsService;

    /**
     * 查询非星级酒店评价列表
     */
    @GetMapping("/list")
    public TableDataInfo list(Nonstarhotelreviews nonstarhotelreviews)
    {
        startPage();
        List<Nonstarhotelreviews> list = nonstarhotelreviewsService.selectNonstarhotelreviewsList(nonstarhotelreviews);
        return getDataTable(list);
    }

    /**
     * 导出非星级酒店评价列表
     */
    @Log(title = "非星级酒店评价", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Nonstarhotelreviews nonstarhotelreviews)
    {
        List<Nonstarhotelreviews> list = nonstarhotelreviewsService.selectNonstarhotelreviewsList(nonstarhotelreviews);
        ExcelUtil<Nonstarhotelreviews> util = new ExcelUtil<Nonstarhotelreviews>(Nonstarhotelreviews.class);
        util.exportExcel(response, list, "非星级酒店评价数据");
    }

    /**
     * 获取非星级酒店评价详细信息
     */
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(nonstarhotelreviewsService.selectNonstarhotelreviewsById(id));
    }

    /**
     * 新增非星级酒店评价
     */
    @Log(title = "非星级酒店评价", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Nonstarhotelreviews nonstarhotelreviews)
    {
        return toAjax(nonstarhotelreviewsService.insertNonstarhotelreviews(nonstarhotelreviews));
    }

    /**
     * 修改非星级酒店评价
     */
    @Log(title = "非星级酒店评价", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Nonstarhotelreviews nonstarhotelreviews)
    {
        return toAjax(nonstarhotelreviewsService.updateNonstarhotelreviews(nonstarhotelreviews));
    }

    /**
     * 删除非星级酒店评价
     */
    @Log(title = "非星级酒店评价", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(nonstarhotelreviewsService.deleteNonstarhotelreviewsByIds(ids));
    }
}
